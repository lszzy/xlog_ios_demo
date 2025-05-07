//
//  ViewController.m
//  xlog_ios_demo
//
//  Created by 逸风 on 2022/3/5.
//

#import "ViewController.h"
#import "JRXlogManager.h"
#import "AppDelegate.h"
#import <SSZipArchive/SSZipArchive.h>
#import <SVProgressHUD/SVProgressHUD.h>

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
}

- (IBAction)uoloadLog:(id)sender {
    [SVProgressHUD show];
    NSString *tmpPath = NSTemporaryDirectory();
    NSString *tmpLogPath = getXlogPath(XlogDirName);
    NSDateFormatter *formatter = [NSDateFormatter new];
    formatter.dateFormat = @"MM-dd_HH-mm";
    NSString *zipPath = [tmpPath stringByAppendingPathComponent:[NSString stringWithFormat:@"logs_%@.zip", [formatter stringFromDate:NSDate.date]]];
    dispatch_async(dispatch_get_global_queue(0, 0), ^{
        BOOL result = [SSZipArchive createZipFileAtPath:zipPath withContentsOfDirectory:tmpLogPath];
        dispatch_async(dispatch_get_main_queue(), ^{
            [SVProgressHUD dismiss];
            if(result) {
                NSURL *url = [NSURL fileURLWithPath:zipPath];
                [self showsUIActivityVControllerWithUrlrs:@[url]];
            } else {
                [SVProgressHUD showErrorWithStatus:@"Zip file fail"];
            }
        });
    });
}

- (void)showsUIActivityVControllerWithUrlrs:(NSArray<NSURL *> *)urls {
    UIActivityViewController *controller = [[UIActivityViewController alloc] initWithActivityItems:urls applicationActivities:nil];
    
    if ([(NSString *)[UIDevice currentDevice].model hasPrefix:@"iPad"]) {
        controller.popoverPresentationController.sourceView = self.view;
        controller.popoverPresentationController.sourceRect = CGRectMake([UIScreen mainScreen].bounds.size.width * 0.5, [UIScreen mainScreen].bounds.size.height, 10, 10);
    }
    [self presentViewController:controller animated:YES completion:^{
    }];
}

- (IBAction)warningClick:(id)sender {
    for (int i = 0; i < 5000; i++) {
        [[JRXlogManager shared] warningLogWithTag:JRDebugMessage Content:@"test warning log message"];
    }
}

- (IBAction)debugClick:(id)sender {
    for (int i = 0; i < 5000; i++) {
        [[JRXlogManager shared] debugLogWithTag:JRDebugMessage Content:@"test debug log message"];
    }
    [[JRXlogManager shared] flushXlog];
}

- (IBAction)infoLogClick:(id)sender {
    [[JRXlogManager shared] flushXlog];
}

- (IBAction)errorClick:(id)sender {
    [[JRXlogManager shared] closeXlog];
}


@end
